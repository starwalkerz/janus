// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title StirpesRegistry
 * @notice The on-chain settlement layer for STIRPES.
 *
 * Each tick is committed as a TickRecord with seven fields. The records
 * are indexed by tick hash, class hash, and clade hash. Queries return
 * the records for a given index. The contract does not verify the
 * contents; it merely attests to their existence and timestamp.
 */
contract StirpesRegistry {
    struct TickRecord {
        bytes32 tickHash;
        bytes32 classHash;
        bytes32 cladeHash;
        bytes32 sessionId;
        uint256 tickIndex;
        uint256 blocktime;
        bytes32 payloadHash;
    }

    /// Per-tick records, keyed by tick hash.
    mapping(bytes32 => TickRecord) public ticks;

    /// Index from class hash to the list of tick hashes with that class.
    mapping(bytes32 => bytes32[]) public classIndex;

    /// Index from clade hash to the list of tick hashes in that clade.
    mapping(bytes32 => bytes32[]) public cladeIndex;

    /// Index from session ID to the list of tick hashes in that session.
    mapping(bytes32 => bytes32[]) public sessionIndex;

    /// Emitted once per commit.
    event TickCommitted(
        bytes32 indexed tickHash,
        bytes32 indexed classHash,
        bytes32 indexed cladeHash,
        bytes32 sessionId,
        uint256 tickIndex,
        uint256 blocktime,
        bytes32 payloadHash
    );

    /// Emitted once per batch.
    event BatchCommitted(
        bytes32 indexed leafSetHash,
        bytes32 indexed treeRootHash,
        uint256 tickCount,
        uint256 blocktime
    );

    /**
     * @notice Commit a batch of tick records.
     * @param tickHashes The tick identifiers.
     * @param classHashes The class hashes.
     * @param cladeHashes The clade hashes.
     * @param sessionIds The session identifiers.
     * @param tickIndices The tick indices within their sessions.
     * @param payloadHashes The payload hashes.
     * @param leafSetHash The hash of the leaf set.
     * @param treeRootHash The hash of the tree topology.
     */
    function commitBatch(
        bytes32[] calldata tickHashes,
        bytes32[] calldata classHashes,
        bytes32[] calldata cladeHashes,
        bytes32[] calldata sessionIds,
        uint256[] calldata tickIndices,
        bytes32[] calldata payloadHashes,
        bytes32 leafSetHash,
        bytes32 treeRootHash
    ) external {
        require(
            tickHashes.length == classHashes.length &&
            tickHashes.length == cladeHashes.length &&
            tickHashes.length == sessionIds.length &&
            tickHashes.length == tickIndices.length &&
            tickHashes.length == payloadHashes.length,
            "length mismatch"
        );

        for (uint256 i = 0; i < tickHashes.length; i++) {
            require(ticks[tickHashes[i]].tickHash == bytes32(0), "tick already committed");

            TickRecord memory record = TickRecord({
                tickHash: tickHashes[i],
                classHash: classHashes[i],
                cladeHash: cladeHashes[i],
                sessionId: sessionIds[i],
                tickIndex: tickIndices[i],
                blocktime: block.timestamp,
                payloadHash: payloadHashes[i]
            });
            ticks[tickHashes[i]] = record;
            classIndex[classHashes[i]].push(tickHashes[i]);
            cladeIndex[cladeHashes[i]].push(tickHashes[i]);
            sessionIndex[sessionIds[i]].push(tickHashes[i]);

            emit TickCommitted(
                tickHashes[i],
                classHashes[i],
                cladeHashes[i],
                sessionIds[i],
                tickIndices[i],
                block.timestamp,
                payloadHashes[i]
            );
        }

        emit BatchCommitted(leafSetHash, treeRootHash, tickHashes.length, block.timestamp);
    }

    /// Get all tick hashes for a class.
    function getTicksByClass(bytes32 classHash) external view returns (bytes32[] memory) {
        return classIndex[classHash];
    }

    /// Get all tick hashes for a clade.
    function getTicksByClade(bytes32 cladeHash) external view returns (bytes32[] memory) {
        return cladeIndex[cladeHash];
    }

    /// Get all tick hashes for a session.
    function getTicksBySession(bytes32 sessionId) external view returns (bytes32[] memory) {
        return sessionIndex[sessionId];
    }
}